from pydantic import BaseModel

class HospitalBase(BaseModel):
    id: int
    name: str
    address: str
    phone: str

class HospitalCreate(BaseModel):
    name: str
    address: str
    phone: str
class HospitalUpdate(HospitalBase):
    pass

class HospitalResponse(HospitalBase):
    id: int

    class Config:
        from_attributes = True
