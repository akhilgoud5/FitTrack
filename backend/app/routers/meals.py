
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Meal, User
from app.schemas import MealCreate, MealOut, NutritionSummary


router = APIRouter(
    prefix="/meals",
    tags=["Nutrition & Meal Tracking"]
)


# 1. ADD MEAL
@router.post("/", response_model=MealOut, status_code=status.HTTP_201_CREATED)
def add_meal(
    meal_data: MealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    meal = Meal(
        user_id=current_user.id,
        meal_type=meal_data.meal_type,
        food_name=meal_data.food_name,
        calories=meal_data.calories,
        protein=meal_data.protein,
        carbs=meal_data.carbs,
        fats=meal_data.fats
    )

    db.add(meal)
    db.commit()
    db.refresh(meal)

    return meal


# 2. VIEW MEAL HISTORY
@router.get("/", response_model=list[MealOut])
def get_meals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    meals = (
        db.query(Meal)
        .filter(Meal.user_id == current_user.id)
        .order_by(Meal.created_at.desc())
        .all()
    )

    return meals


# 3. DAILY NUTRITION SUMMARY
@router.get("/daily-summary", response_model=NutritionSummary)
def get_daily_summary(
    summary_date: date = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    selected_date = summary_date or date.today()

    totals = db.query(
        func.count(Meal.id),
        func.coalesce(func.sum(Meal.calories), 0),
        func.coalesce(func.sum(Meal.protein), 0),
        func.coalesce(func.sum(Meal.carbs), 0),
        func.coalesce(func.sum(Meal.fats), 0)
    ).filter(
        Meal.user_id == current_user.id,
        func.date(Meal.created_at) == selected_date
    ).first()

    return NutritionSummary(
        date=selected_date,
        total_meals=totals[0],
        total_calories=totals[1],
        total_protein=totals[2],
        total_carbs=totals[3],
        total_fats=totals[4]
    )
