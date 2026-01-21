from pydantic import BaseModel

class DoctorCreate(BaseModel):
    name: str
    department: str

class DoctorResponse(DoctorCreate):
    id: int

    class Config:
        from_attributes = True
