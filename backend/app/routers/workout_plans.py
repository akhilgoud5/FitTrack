
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import WorkoutPlan, User
from app.schemas import (
    WorkoutPlanCreate,
    WorkoutPlanUpdate,
    WorkoutPlanOut
)
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/workout-plans",
    tags=["Workout Plans"]
)


# 1. CREATE WORKOUT PLAN
@router.post(
    "/",
    response_model=WorkoutPlanOut,
    status_code=status.HTTP_201_CREATED
)
def create_workout_plan(
    data: WorkoutPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if data.scheduled_date < date.today():
        raise HTTPException(
            status_code=400,
            detail="Scheduled date cannot be in the past"
        )

    plan = WorkoutPlan(
        user_id=current_user.id,
        title=data.title,
        description=data.description,
        scheduled_date=data.scheduled_date
    )

    try:
        db.add(plan)
        db.commit()
        db.refresh(plan)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to create workout plan"
        )

    return plan


# 2. GET ALL MY WORKOUT PLANS
@router.get("/", response_model=list[WorkoutPlanOut])
def get_my_workout_plans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == current_user.id
    ).order_by(WorkoutPlan.scheduled_date.asc()).all()


# 3. GET UPCOMING WORKOUTS
@router.get("/upcoming", response_model=list[WorkoutPlanOut])
def get_upcoming_workouts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == current_user.id,
        WorkoutPlan.scheduled_date >= date.today()
    ).order_by(WorkoutPlan.scheduled_date.asc()).all()


# 4. GET WORKOUT PLAN BY ID
@router.get("/{plan_id}", response_model=WorkoutPlanOut)
def get_workout_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = db.query(WorkoutPlan).filter(
        WorkoutPlan.id == plan_id,
        WorkoutPlan.user_id == current_user.id
    ).first()

    if plan is None:
        raise HTTPException(
            status_code=404,
            detail="Workout plan not found"
        )

    return plan


# 5. UPDATE WORKOUT PLAN
@router.put("/{plan_id}", response_model=WorkoutPlanOut)
def update_workout_plan(
    plan_id: int,
    data: WorkoutPlanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = db.query(WorkoutPlan).filter(
        WorkoutPlan.id == plan_id,
        WorkoutPlan.user_id == current_user.id
    ).first()

    if plan is None:
        raise HTTPException(
            status_code=404,
            detail="Workout plan not found"
        )

    if data.scheduled_date < date.today():
        raise HTTPException(
            status_code=400,
            detail="Scheduled date cannot be in the past"
        )

    plan.title = data.title
    plan.description = data.description
    plan.scheduled_date = data.scheduled_date

    try:
        db.commit()
        db.refresh(plan)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to update workout plan"
        )

    return plan


# 6. DELETE WORKOUT PLAN
@router.delete("/{plan_id}")
def delete_workout_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = db.query(WorkoutPlan).filter(
        WorkoutPlan.id == plan_id,
        WorkoutPlan.user_id == current_user.id
    ).first()

    if plan is None:
        raise HTTPException(
            status_code=404,
            detail="Workout plan not found"
        )

    try:
        db.delete(plan)
        db.commit()

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to delete workout plan"
        )

    return {
        "message": "Workout plan deleted successfully"
    }
