from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from app.database import get_db
from models.document_access import DocumentAccessRequest
from schemas.document_access import AccessRequestCreate
from auth.jwt import get_current_user

router = APIRouter(prefix="/access", tags=["Document Access"])

@router.post("/request")
def request_access(
    data: AccessRequestCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    if user.role != "hospital":
        raise HTTPException(status_code=403, detail="Only hospitals can request access")

    access = DocumentAccessRequest(
        patient_id=data.patient_id,
        hospital_id=user.id,
        document_url=data.document_url
    )
    db.add(access)
    db.commit()
    db.refresh(access)

    return {"message": "Access request sent"}

@router.get("/patient/requests")
def get_requests(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=50),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    if user.role != "patient":
        raise HTTPException(status_code=403)

    offset = (page - 1) * limit

    total = db.query(DocumentAccessRequest).filter(
        DocumentAccessRequest.patient_id == user.id
    ).count()

    requests = (
        db.query(DocumentAccessRequest)
        .filter(DocumentAccessRequest.patient_id == user.id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": requests
    }
@router.put("/request/{request_id}")
def update_request(
    request_id: int,
    action: str,  # approve / deny
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    access = db.query(DocumentAccessRequest).filter(
        DocumentAccessRequest.id == request_id,
        DocumentAccessRequest.patient_id == user.id
    ).first()

    if not access:
        raise HTTPException(status_code=404)

    if action not in ["approve", "deny"]:
        raise HTTPException(status_code=400)

    access.status = "approved" if action == "approve" else "denied"
    db.commit()

    return {"message": f"Request {action}d"}
