
from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User, Workout , Goal

router = APIRouter(
    prefix="/analytics",
    tags=["Workout Analytics"]
)


# 1. WORKOUT CATEGORY ANALYTICS
@router.get("/categories")
def category_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = db.query(
        Workout.category,
        func.count(Workout.id).label("total_workouts"),
        func.sum(Workout.calories_burned).label("total_calories")
    ).filter(
        Workout.user_id == current_user.id
    ).group_by(
        Workout.category
    ).all()

    return [
        {
            "category": row.category,
            "total_workouts": row.total_workouts,
            "total_calories": row.total_calories or 0
        }
        for row in results
    ]


# 2. WORKOUT PERFORMANCE ANALYTICS
@router.get("/performance")
def workout_performance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total_workouts = db.query(func.count(Workout.id)).filter(
        Workout.user_id == current_user.id
    ).scalar()

    total_calories = db.query(
        func.sum(Workout.calories_burned)
    ).filter(
        Workout.user_id == current_user.id
    ).scalar()

    total_duration = db.query(
        func.sum(Workout.duration)
    ).filter(
        Workout.user_id == current_user.id
    ).scalar()

    return {
        "total_workouts": total_workouts or 0,
        "total_calories": total_calories or 0,
        "total_duration": total_duration or 0
    }


# 3. LAST 7 DAYS ANALYTICS
@router.get("/last-7-days")
def last_7_days_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    start_date = date.today() - timedelta(days=6)

    results = db.query(
        Workout.workout_date,
        func.count(Workout.id).label("total_workouts"),
        func.sum(Workout.calories_burned).label("total_calories")
    ).filter(
        Workout.user_id == current_user.id,
        Workout.workout_date >= start_date,
        Workout.workout_date <= date.today()
    ).group_by(
        Workout.workout_date
    ).order_by(
        Workout.workout_date
    ).all()

    return [
        {
            "date": row.workout_date,
            "total_workouts": row.total_workouts,
            "total_calories": row.total_calories or 0
        }
        for row in results
    ]

# 4. GOAL COMPLETION ANALYTICS

@router.get("/goal-completion")
def goal_completion_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goals = db.query(Goal).filter(
        Goal.user_id == current_user.id
    ).all()

    total_goals = len(goals)

    completed_goals = sum(
        1 for goal in goals
        if goal.current_value >= goal.target_value
    )

    completion_rate = (
        (completed_goals / total_goals) * 100
        if total_goals > 0 else 0
    )

    return {
        "total_goals": total_goals,
        "completed_goals": completed_goals,
        "pending_goals": total_goals - completed_goals,
        "completion_rate": round(completion_rate, 2)
    }

# 5. MONTHLY WORKOUT ANALYTICS

@router.get("/monthly")
def monthly_workout_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    start_date = date.today() - timedelta(days=180)

    results = db.query(
        func.strftime("%Y-%m", Workout.workout_date).label("month"),
        func.count(Workout.id).label("total_workouts"),
        func.sum(Workout.calories_burned).label("total_calories"),
        func.sum(Workout.duration).label("total_duration")
    ).filter(
        Workout.user_id == current_user.id,
        Workout.workout_date >= start_date
    ).group_by(
        func.strftime("%Y-%m", Workout.workout_date)
    ).order_by(
        func.strftime("%Y-%m", Workout.workout_date)
    ).all()

    return [
        {
            "month": row.month,
            "total_workouts": row.total_workouts,
            "total_calories": row.total_calories or 0,
            "total_duration": row.total_duration or 0
        }
        for row in results
    ]

# 6. WORKOUT CONSISTENCY ANALYTICS

@router.get("/consistency")
def workout_consistency(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()
    start_date = today - timedelta(days=29)

    active_days = db.query(
        func.count(func.distinct(Workout.workout_date))
    ).filter(
        Workout.user_id == current_user.id,
        Workout.workout_date >= start_date,
        Workout.workout_date <= today
    ).scalar()

    total_days = 30

    consistency_rate = (
        (active_days / total_days) * 100
    )

    return {
        "period": "Last 30 days",
        "total_days": total_days,
        "active_days": active_days or 0,
        "inactive_days": total_days - (active_days or 0),
        "consistency_rate": round(consistency_rate, 2)
    }
