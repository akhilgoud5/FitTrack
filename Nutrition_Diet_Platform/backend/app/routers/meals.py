
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Meal, User
from app.schemas import MealCreate, MealOut, NutritionSummary
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/meals",
    tags=["Meal & Nutrition Tracking"]
)


# Add Meal
@router.post("/", response_model=MealOut, status_code=201)
def add_meal(
    meal_data: MealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_meal = Meal(
        user_id=current_user.id,
        meal_type=meal_data.meal_type,
        food_name=meal_data.food_name,
        calories=meal_data.calories,
        protein=meal_data.protein,
        carbs=meal_data.carbs,
        fats=meal_data.fats
    )

    db.add(new_meal)
    db.commit()
    db.refresh(new_meal)

    return new_meal


# View Meal History
@router.get("/", response_model=list[MealOut])
def get_meals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Meal).filter(
        Meal.user_id == current_user.id
    ).order_by(Meal.created_at.desc()).all()


# Daily Nutrition Summary
@router.get("/daily-summary", response_model=NutritionSummary)
def daily_nutrition_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()

    summary = db.query(
        func.coalesce(func.sum(Meal.calories), 0).label("total_calories"),
        func.coalesce(func.sum(Meal.protein), 0).label("total_protein"),
        func.coalesce(func.sum(Meal.carbs), 0).label("total_carbs"),
        func.coalesce(func.sum(Meal.fats), 0).label("total_fats"),
        func.count(Meal.id).label("total_meals")
    ).filter(
        Meal.user_id == current_user.id,
        func.date(Meal.created_at) == today
    ).first()

    return {
        "total_calories": summary.total_calories,
        "total_protein": summary.total_protein,
        "total_carbs": summary.total_carbs,
        "total_fats": summary.total_fats,
        "total_meals": summary.total_meals
    }
