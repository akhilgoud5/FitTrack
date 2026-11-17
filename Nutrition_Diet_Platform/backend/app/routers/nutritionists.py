
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Nutritionist, Consultation, User
from app.schemas import (
    NutritionistCreate,
    NutritionistOut,
    ConsultationCreate,
    ConsultationOut
)
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/nutritionists",
    tags=["Nutritionist Consultation"]
)


# Add Nutritionist
@router.post("/", response_model=NutritionistOut, status_code=201)
def create_nutritionist(
    nutritionist_data: NutritionistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_nutritionist = Nutritionist(
        name=nutritionist_data.name,
        specialization=nutritionist_data.specialization,
        experience=nutritionist_data.experience,
        contact_info=nutritionist_data.contact_info
    )

    db.add(new_nutritionist)
    db.commit()
    db.refresh(new_nutritionist)

    return new_nutritionist


# View All Nutritionists
@router.get("/", response_model=list[NutritionistOut])
def get_nutritionists(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Nutritionist).all()


# Book Consultation
@router.post("/book", response_model=ConsultationOut, status_code=201)
def book_consultation(
    booking_data: ConsultationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    nutritionist = db.query(Nutritionist).filter(
        Nutritionist.id == booking_data.nutritionist_id
    ).first()

    if not nutritionist:
        raise HTTPException(
            status_code=404,
            detail="Nutritionist not found"
        )

    scheduled_time = booking_data.scheduled_time

    if scheduled_time.tzinfo is None:
        scheduled_time = scheduled_time.replace(tzinfo=timezone.utc)

    if scheduled_time <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="Consultation time must be in the future"
        )

    new_consultation = Consultation(
        user_id=current_user.id,
        nutritionist_id=nutritionist.id,
        scheduled_time=scheduled_time,
        status="PENDING"
    )

    db.add(new_consultation)
    db.commit()
    db.refresh(new_consultation)

    return new_consultation


# View My Consultation History
@router.get("/my-consultations", response_model=list[ConsultationOut])
def get_my_consultations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Consultation).filter(
        Consultation.user_id == current_user.id
    ).order_by(
        Consultation.scheduled_time.desc()
    ).all()


# View Nutritionist Details
@router.get("/{nutritionist_id}", response_model=NutritionistOut)
def get_nutritionist(
    nutritionist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    nutritionist = db.query(Nutritionist).filter(
        Nutritionist.id == nutritionist_id
    ).first()

    if not nutritionist:
        raise HTTPException(
            status_code=404,
            detail="Nutritionist not found"
        )

    return nutritionist
