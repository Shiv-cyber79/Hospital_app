from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    age = Column(Integer)
    phone = Column(String(20))
    address = Column(String(255))