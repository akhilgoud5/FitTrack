
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Workout, User, Progress
from app.schemas import ProgressOut
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/progress",
    tags=["Progress"]
)


# 1. GET TODAY'S PROGRESS
@router.get("/today")
def get_today_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()

    total_workouts = db.query(Workout).filter(
        Workout.user_id == current_user.id,
        Workout.workout_date == today
    ).count()

    total_calories = db.query(
        func.coalesce(
            func.sum(Workout.calories_burned), 0
        )
    ).filter(
        Workout.user_id == current_user.id,
        Workout.workout_date == today
    ).scalar()

    return {
        "date": today,
        "total_workouts": total_workouts,
        "total_calories": total_calories
    }


# 2. GET PROGRESS HISTORY
@router.get("/", response_model=list[ProgressOut])
def get_progress_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Progress).filter(
        Progress.user_id == current_user.id
    ).order_by(Progress.date.desc()).all()
