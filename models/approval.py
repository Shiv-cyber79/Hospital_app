from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Approval(Base):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    status = Column(String(20), default="pending")  