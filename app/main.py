from fastapi import FastAPI
from app.database import Base, engine
from routers import patient, doctor, appointment, auth,hospital,approval,sidebar

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital Management System")

app.include_router(auth.router)

app.include_router(auth.router)
app.include_router(patient.router)
app.include_router(doctor.router)
app.include_router(appointment.router)
app.include_router(hospital.router)
app.include_router(approval.router)
app.include_router(sidebar.router)
