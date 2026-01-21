from pydantic import BaseModel

class ApprovalCreate(BaseModel):
    hospital_id: int

class ApprovalResponse(BaseModel):
    id: int
    patient_id: int
    hospital_id: int
    status: str

    class Config:
        from_attributes = True
