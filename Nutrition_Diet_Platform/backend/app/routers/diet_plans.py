
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import DietPlan, UserDietPlan, User
from app.schemas import (
    DietPlanCreate,
    DietPlanOut,
    UserDietPlanCreate,
    UserDietPlanOut
)
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/diet-plans",
    tags=["Diet Plans"]
)


# Create Diet Plan
@router.post("/", response_model=DietPlanOut, status_code=201)
def create_diet_plan(
    plan_data: DietPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_plan = DietPlan(
        title=plan_data.title,
        description=plan_data.description,
        goal_type=plan_data.goal_type,
        daily_calories=plan_data.daily_calories,
        duration=plan_data.duration
    )

    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)

    return new_plan


# View All Diet Plans
@router.get("/", response_model=list[DietPlanOut])
def get_all_diet_plans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(DietPlan).all()


# View My Assigned Diet Plans
@router.get("/my-plans", response_model=list[UserDietPlanOut])
def get_my_diet_plans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(UserDietPlan).filter(
        UserDietPlan.user_id == current_user.id
    ).all()


# Assign Diet Plan to Logged-in User
@router.post("/assign", response_model=UserDietPlanOut, status_code=201)
def assign_diet_plan(
    assignment: UserDietPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = db.query(DietPlan).filter(
        DietPlan.id == assignment.diet_plan_id
    ).first()

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Diet plan not found"
        )

    existing = db.query(UserDietPlan).filter(
        UserDietPlan.user_id == current_user.id,
        UserDietPlan.diet_plan_id == assignment.diet_plan_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Diet plan already assigned"
        )

    new_assignment = UserDietPlan(
        user_id=current_user.id,
        diet_plan_id=assignment.diet_plan_id
    )

    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return new_assignment


# View Diet Plan Details
@router.get("/{plan_id}", response_model=DietPlanOut)
def get_diet_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = db.query(DietPlan).filter(
        DietPlan.id == plan_id
    ).first()

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Diet plan not found"
        )

    return plan
