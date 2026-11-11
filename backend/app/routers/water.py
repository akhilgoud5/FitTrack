
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.dependencies import get_current_user
from app.models import WaterIntake, User
from app.schemas import (
    WaterIntakeCreate,
    WaterIntakeOut,
    WaterIntakeSummary
)

router = APIRouter(
    prefix="/water",
    tags=["Water Intake Tracker"]
)


# 1. ADD WATER INTAKE
@router.post(
    "/",
    response_model=WaterIntakeOut,
    status_code=status.HTTP_201_CREATED
)
def add_water(
    water_data: WaterIntakeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    water = WaterIntake(
        user_id=current_user.id,
        amount_ml=water_data.amount_ml
    )

    db.add(water)
    db.commit()
    db.refresh(water)

    return water


# 2. VIEW WATER HISTORY
@router.get("/", response_model=list[WaterIntakeOut])
def get_water_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(WaterIntake)
        .filter(WaterIntake.user_id == current_user.id)
        .order_by(WaterIntake.logged_at.desc())
        .all()
    )


# 3. DAILY WATER SUMMARY
@router.get(
    "/daily-summary",
    response_model=WaterIntakeSummary
)
def get_water_summary(
    summary_date: date = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    selected_date = summary_date or date.today()

    total = db.query(
        func.coalesce(func.sum(WaterIntake.amount_ml), 0)
    ).filter(
        WaterIntake.user_id == current_user.id,
        func.date(WaterIntake.logged_at) == selected_date
    ).scalar()

    daily_goal = 2500

    return WaterIntakeSummary(
        date=selected_date,
        total_water_ml=total,
        daily_goal_ml=daily_goal,
        remaining_ml=max(daily_goal - total, 0)
    )
