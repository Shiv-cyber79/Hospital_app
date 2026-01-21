from pydantic import BaseModel

class SidebarResponse(BaseModel):
    id: int
    title: str
    path: str

    class Config:
        from_attributes = True
