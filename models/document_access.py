from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from app.database import Base
import enum

class AccessStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    denied = "denied"

class DocumentAccessRequest(Base):
    __tablename__ = "document_access_requests"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    document_url = Column(String(255))
    status = Column(Enum(AccessStatus), default=AccessStatus.pending)
