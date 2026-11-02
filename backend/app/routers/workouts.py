
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Workout, User
from app.schemas import WorkoutCreate, WorkoutOut, WorkoutUpdate
from app.dependencies import get_current_user
from app.progress_utils import sync_daily_progress


router = APIRouter(
    prefix="/workouts",
    tags=["Workouts"]
)


# 1. CREATE WORKOUT
@router.post(
    "/",
    response_model=WorkoutOut,
    status_code=status.HTTP_201_CREATED
)
def create_workout(
    data: WorkoutCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workout = Workout(
        user_id=current_user.id,
        workout_name=data.workout_name,
        category=data.category,
        duration=data.duration,
        calories_burned=data.calories_burned,
        workout_date=data.workout_date
    )

    try:
        db.add(workout)
        db.commit()
        db.refresh(workout)

        sync_daily_progress(
            db,
            current_user.id,
            workout.workout_date
        )
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to create workout"
        )

    return workout


# 2. GET ALL MY WORKOUTS
@router.get("/", response_model=list[WorkoutOut])
def get_my_workouts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Workout).filter(
        Workout.user_id == current_user.id
    ).order_by(Workout.workout_date.desc()).all()


# 3. SEARCH WORKOUTS
@router.get("/search", response_model=list[WorkoutOut])
def search_workouts(
    keyword: str = Query(..., min_length=1, max_length=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    keyword = keyword.strip()

    if not keyword:
        raise HTTPException(
            status_code=400,
            detail="Search keyword cannot be empty"
        )

    return db.query(Workout).filter(
        Workout.user_id == current_user.id,
        Workout.workout_name.ilike(f"%{keyword}%")
    ).all()


# 4. FILTER BY CATEGORY
@router.get("/filter/category", response_model=list[WorkoutOut])
def filter_by_category(
    category: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    allowed_categories = ["Cardio", "Strength", "Yoga"]

    if category.strip().lower() not in [
        item.lower() for item in allowed_categories
    ]:
        raise HTTPException(
            status_code=400,
            detail="Invalid category"
        )

    return db.query(Workout).filter(
        Workout.user_id == current_user.id,
        Workout.category.ilike(category.strip())
    ).all()


# 5. FILTER BY DATE RANGE
@router.get("/filter/date", response_model=list[WorkoutOut])
def filter_by_date(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be after end date"
        )

    return db.query(Workout).filter(
        Workout.user_id == current_user.id,
        Workout.workout_date >= start_date,
        Workout.workout_date <= end_date
    ).order_by(Workout.workout_date.desc()).all()


# 6. GET WORKOUT BY ID
@router.get("/{workout_id}", response_model=WorkoutOut)
def get_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workout = db.query(Workout).filter(
        Workout.id == workout_id,
        Workout.user_id == current_user.id
    ).first()

    if workout is None:
        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )

    return workout


# 7. UPDATE WORKOUT
@router.put("/{workout_id}", response_model=WorkoutOut)
def update_workout(
    workout_id: int,
    data: WorkoutUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workout = db.query(Workout).filter(
        Workout.id == workout_id,
        Workout.user_id == current_user.id
    ).first()

    if workout is None:
        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )

    old_workout_date = workout.workout_date

    workout.workout_name = data.workout_name
    workout.category = data.category
    workout.duration = data.duration
    workout.calories_burned = data.calories_burned
    workout.workout_date = data.workout_date

    try:
        db.commit()
        db.refresh(workout)

        sync_daily_progress(
            db,
            current_user.id,
            old_workout_date
        )

        if workout.workout_date != old_workout_date:
            sync_daily_progress(
                db,
                current_user.id,
                workout.workout_date
            )

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to update workout"
        )

    return workout


# 8. DELETE WORKOUT
@router.delete("/{workout_id}")
def delete_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workout = db.query(Workout).filter(
        Workout.id == workout_id,
        Workout.user_id == current_user.id
    ).first()

    if workout is None:
        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )

    workout_date = workout.workout_date

    try:
        db.delete(workout)
        db.commit()

        sync_daily_progress(
            db,
            current_user.id,
            workout_date
        )

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to delete workout"
        )

    return {
        "message": "Workout deleted successfully"
    }
