
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Exercise
from app.schemas import ExerciseCreate, ExerciseOut
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/exercises",
    tags=["Exercise Library"]
)


# 1. ADD EXERCISE
@router.post(
    "/",
    response_model=ExerciseOut,
    status_code=status.HTTP_201_CREATED
)
def create_exercise(
    data: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    exercise = Exercise(
        name=data.name,
        category=data.category,
        description=data.description,
        duration=data.duration
    )

    try:
        db.add(exercise)
        db.commit()
        db.refresh(exercise)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to create exercise"
        )

    return exercise


# 2. GET ALL EXERCISES
@router.get("/", response_model=list[ExerciseOut])
def get_exercises(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Exercise).order_by(
        Exercise.name.asc()
    ).all()


# 3. SEARCH EXERCISES
@router.get("/search", response_model=list[ExerciseOut])
def search_exercises(
    keyword: str = Query(..., min_length=1, max_length=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    keyword = keyword.strip()

    if not keyword:
        raise HTTPException(
            status_code=400,
            detail="Search keyword cannot be empty"
        )

    return db.query(Exercise).filter(
        Exercise.name.ilike(f"%{keyword}%")
    ).all()


# 4. FILTER BY CATEGORY
@router.get("/filter/category", response_model=list[ExerciseOut])
def filter_exercises_by_category(
    category: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    allowed_categories = ["Cardio", "Strength", "Yoga"]

    category = category.strip()

    if category.lower() not in [
        item.lower() for item in allowed_categories
    ]:
        raise HTTPException(
            status_code=400,
            detail="Invalid exercise category"
        )

    return db.query(Exercise).filter(
        Exercise.category.ilike(category)
    ).all()


# 5. GET EXERCISE BY ID
@router.get("/{exercise_id}", response_model=ExerciseOut)
def get_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    exercise = db.query(Exercise).filter(
        Exercise.id == exercise_id
    ).first()

    if exercise is None:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found"
        )

    return exercise


# 6. DELETE EXERCISE
@router.delete("/{exercise_id}")
def delete_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    exercise = db.query(Exercise).filter(
        Exercise.id == exercise_id
    ).first()

    if exercise is None:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found"
        )

    try:
        db.delete(exercise)
        db.commit()

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to delete exercise"
        )

    return {
        "message": "Exercise deleted successfully"
    }
