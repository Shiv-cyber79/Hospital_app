from fastapi import APIRouter, Depends
from auth.jwt import get_current_user

router = APIRouter(prefix="/sidebar", tags=["Sidebar"])

@router.get("/")
def sidebar(user=Depends(get_current_user)):
    if user["role"] == "admin":
        return ["Dashboard", "Hospitals", "Users"]
    return ["Dashboard", "My Patients"]
