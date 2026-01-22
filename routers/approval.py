from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from models.hospital import Hospital
from models.patient import Patient
from auth.roles import require_role
from models.approval import Approval
from auth.jwt import get_current_user


router = APIRouter(
    prefix="/patients",
    tags=["Patient Approvals"]
)

@router.post("/request/{patient_id}")
def request_access(
    patient_id: int,
    hospital_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("doctor"))
):
    approval = Approval(
        patient_id=patient_id,
        hospital_id=hospital_id,
        status="pending"
    )
    db.add(approval)
    db.commit()
    return {"message": "Access requested"}

@router.post("/approve/{approval_id}")
def approve_access(
    approval_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("patient"))
):
    approval = db.query(Approval).filter(
        Approval.id == approval_id
    ).first()

    if not approval:
        raise HTTPException(status_code=404, detail="Not found")

    approval.status = "approved"
    db.commit()
    return {"message": "Access approved"}
