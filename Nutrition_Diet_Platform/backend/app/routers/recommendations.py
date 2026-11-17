
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import DietPlan, User
from app.schemas import (
    DietRecommendationRequest,
    DietRecommendationOut
)
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/recommendations",
    tags=["Diet Recommendations"]
)


# Basic AI Diet Recommendation
@router.post(
    "/recommend",
    response_model=DietRecommendationOut
)
def recommend_diet_plans(
    request: DietRecommendationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Activity-based calorie matching tolerance
    activity_tolerance = {
        "Sedentary": 150,
        "Light": 200,
        "Moderate": 250,
        "Active": 300,
        "Very Active": 350
    }

    tolerance = activity_tolerance[request.activity_level]

    # Find plans matching the user's goal
    plans = db.query(DietPlan).filter(
        DietPlan.goal_type == request.goal_type
    ).all()

    # Match plans based on calorie requirement
    recommended_plans = [
        plan for plan in plans
        if abs(
            plan.daily_calories - request.calories_requirement
        ) <= tolerance
    ]

    # Sort by closest calorie requirement
    recommended_plans.sort(
        key=lambda plan: abs(
            plan.daily_calories - request.calories_requirement
        )
    )

    return {
        "goal_type": request.goal_type,
        "calories_requirement": request.calories_requirement,
        "activity_level": request.activity_level,
        "recommended_plans": recommended_plans
    }
