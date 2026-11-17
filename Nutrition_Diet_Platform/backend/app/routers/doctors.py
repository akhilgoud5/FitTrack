
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.routers import (  auth, diet_plans, meals, subscriptions, nutritionists, recommendations, notifications, doctors )

from app.database import get_db
from app.models import Doctor, DoctorAppointment, User
from app.schemas import (
    DoctorCreate,
    DoctorOut,
    DoctorAppointmentCreate,
    DoctorAppointmentOut
)
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/doctors",
    tags=["Doctor Support & Appointments"]
)


# Add Doctor
@router.post("/", response_model=DoctorOut, status_code=201)
def create_doctor(
    doctor_data: DoctorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_doctor = Doctor(**doctor_data.model_dump())

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor


# View All Doctors
@router.get("/", response_model=list[DoctorOut])
def get_doctors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Doctor).order_by(Doctor.id.desc()).all()


# View Doctor Profile
@router.get("/{doctor_id}", response_model=DoctorOut)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return doctor


# Book Appointment
@router.post("/appointments/book", response_model=DoctorAppointmentOut, status_code=201)
def book_appointment(
    appointment_data: DoctorAppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == appointment_data.doctor_id
    ).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if doctor.availability_status != "AVAILABLE":
        raise HTTPException(status_code=400, detail="Doctor is not available")

    new_appointment = DoctorAppointment(
        user_id=current_user.id,
        doctor_id=appointment_data.doctor_id,
        appointment_date=appointment_data.appointment_date,
        time_slot=appointment_data.time_slot
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment


# View My Appointments
@router.get("/appointments/my-appointments", response_model=list[DoctorAppointmentOut])
def get_my_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(DoctorAppointment).filter(
        DoctorAppointment.user_id == current_user.id
    ).order_by(DoctorAppointment.appointment_date.desc()).all()
