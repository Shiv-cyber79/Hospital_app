from pydantic import BaseModel

class AccessRequestCreate(BaseModel):
    patient_id: int
    document_url: str

class AccessRequestResponse(BaseModel):
    id: int
    patient_id: int
    hospital_id: int
    document_url: str
    status: str
