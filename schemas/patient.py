from pydantic import BaseModel
from typing import Optional

class PatientCreate(BaseModel):
    age: int
    phone: str
    address: str

class PatientUpdate(BaseModel):
    age: Optional[int] = None
    phone: Optional[str] = None
    address: Optional[str] = None
class PatientResponse(PatientUpdate):
    id: int

    class Config:
        from_attributes = True
