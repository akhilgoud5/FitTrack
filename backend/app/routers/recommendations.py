
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User, Workout, Goal, Exercise

router = APIRouter(
    prefix="/recommendations",
    tags=["AI Workout Suggestions"]
)


@router.get("/workouts")
def get_workout_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get user's fitness goal
    goal = (
        db.query(Goal)
        .filter(Goal.user_id == current_user.id)
        .order_by(Goal.created_at.desc())
        .first()
    )

    # Get recent workouts
    recent_workouts = (
        db.query(Workout)
        .filter(Workout.user_id == current_user.id)
        .order_by(Workout.workout_date.desc())
        .limit(5)
        .all()
    )

    # Select recommended category
    if goal and goal.goal_type == "Weight Loss":
        category = "Cardio"

    elif goal and goal.goal_type == "Muscle Gain":
        category = "Strength"

    else:
        category = "Yoga"

    # Find matching exercises
    exercises = (
        db.query(Exercise)
        .filter(Exercise.category == category)
        .limit(5)
        .all()
    )

    return {
        "user_id": current_user.id,
        "fitness_goal": goal.goal_type if goal else "General Fitness",
        "recommended_category": category,
        "recent_workouts": [
            workout.workout_name
            for workout in recent_workouts
        ],
        "recommendations": [
            {
                "id": exercise.id,
                "name": exercise.name,
                "category": exercise.category,
                "description": exercise.description,
                "duration": exercise.duration
            }
            for exercise in exercises
        ]
    }
