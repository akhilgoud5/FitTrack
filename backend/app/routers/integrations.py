
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User, Workout
from typing import Literal
router = APIRouter(
    prefix="/integrations",
    tags=["Third-Party Integrations"]
)

class FitnessSyncRequest(BaseModel):
    provider: Literal["Google Fit", "Apple Health"]
    workout_name: str
    category: Literal["Cardio", "Strength", "Yoga"]
    duration: int = Field(gt=0)
    calories_burned: int = Field(ge=0)
    workout_date: date

@router.post("/sync")
def sync_fitness_data(
    data: FitnessSyncRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if data.provider not in ["Google Fit", "Apple Health"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported fitness provider"
        )

    workout = Workout(
        user_id=current_user.id,
        workout_name=data.workout_name,
        category=data.category,
        duration=data.duration,
        calories_burned=data.calories_burned,
        workout_date=data.workout_date
    )

    db.add(workout)
    db.commit()
    db.refresh(workout)

    return {
        "message": "Fitness data synced successfully",
        "provider": data.provider,
        "workout_id": workout.id,
        "workout_name": workout.workout_name,
        "duration": workout.duration,
        "calories_burned": workout.calories_burned,
        "status": "SYNCED"
    }


@router.get("/status")
def integration_status(
    current_user: User = Depends(get_current_user)
):
    return {
        "user_id": current_user.id,
        "supported_providers": [
            "Google Fit",
            "Apple Health"
        ],
        "message": "Integration service is available"
    }
