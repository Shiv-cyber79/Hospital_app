from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from models.approval import Approval
from auth.jwt import get_current_user


router = APIRouter(
    prefix="/patients",
    tags=["Patient Approvals"]
)

@router.post("/patients/request/{patient_id}")
def request_access(
    patient_id: int,
    hospital_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    patient = db.query(patient).filter(patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    hospital = db.query(hospital).filter(hospital.id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")

 
    approval = Approval(
        patient_id=patient_id,
        hospital_id=hospital_id,
        status="pending"
    )
    db.add(approval)
    db.commit()
    db.refresh(approval)

    return approval

@router.post("/approve/{approval_id}")
def approve_request(
    approval_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    approval = db.query(Approval).get(approval_id)
    approval.status = "approved"
    db.commit()
    return {"message": "Approved"}