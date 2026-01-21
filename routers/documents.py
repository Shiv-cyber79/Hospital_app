from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from auth.jwt import get_current_user
from sqlalchemy.orm import Session
from app.database import get_db
from models.document_access import DocumentAccessRequest

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.get("/view")
def view_document(
    document_url: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    access = db.query(DocumentAccessRequest).filter(
        DocumentAccessRequest.document_url == document_url,
        DocumentAccessRequest.hospital_id == user.id,
        DocumentAccessRequest.status == "approved"
    ).first()

    if not access:
        return FileResponse("static/unauthorized.png")

    return FileResponse(document_url)
