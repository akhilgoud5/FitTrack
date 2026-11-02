
from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Workout, User
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/reports",
    tags=["Reports & Analytics"]
)


# 1. OVERALL WORKOUT SUMMARY
@router.get("/summary")
def get_workout_summary(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be after end date"
        )

    query = db.query(Workout).filter(
        Workout.user_id == current_user.id
    )

    if start_date:
        query = query.filter(
            Workout.workout_date >= start_date
        )

    if end_date:
        query = query.filter(
            Workout.workout_date <= end_date
        )

    total_workouts = query.count()

    total_calories = query.with_entities(
        func.coalesce(func.sum(Workout.calories_burned), 0)
    ).scalar()

    total_duration = query.with_entities(
        func.coalesce(func.sum(Workout.duration), 0)
    ).scalar()

    average_calories = (
        total_calories / total_workouts
        if total_workouts > 0 else 0
    )

    return {
        "total_workouts": total_workouts,
        "total_calories": total_calories,
        "total_duration_minutes": total_duration,
        "average_calories": round(average_calories, 2)
    }


# 2. WORKOUT CATEGORY ANALYSIS
@router.get("/categories")
def get_category_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = db.query(
        Workout.category,
        func.count(Workout.id).label("total_workouts"),
        func.coalesce(
            func.sum(Workout.calories_burned), 0
        ).label("total_calories")
    ).filter(
        Workout.user_id == current_user.id
    ).group_by(
        Workout.category
    ).all()

    return [
        {
            "category": row.category,
            "total_workouts": row.total_workouts,
            "total_calories": row.total_calories
        }
        for row in results
    ]


# 3. WEEKLY WORKOUT REPORT
@router.get("/weekly")
def get_weekly_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())

    workouts = db.query(Workout).filter(
        Workout.user_id == current_user.id,
        Workout.workout_date >= week_start,
        Workout.workout_date <= today
    ).all()

    return {
        "week_start": week_start,
        "week_end": today,
        "total_workouts": len(workouts),
        "total_calories": sum(
            w.calories_burned for w in workouts
        ),
        "total_duration_minutes": sum(
            w.duration for w in workouts
        )
    }


# 4. MONTHLY WORKOUT REPORT
@router.get("/monthly")
def get_monthly_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()
    month_start = today.replace(day=1)

    workouts = db.query(Workout).filter(
        Workout.user_id == current_user.id,
        Workout.workout_date >= month_start,
        Workout.workout_date <= today
    ).all()

    return {
        "month": today.month,
        "year": today.year,
        "total_workouts": len(workouts),
        "total_calories": sum(
            w.calories_burned for w in workouts
        ),
        "total_duration_minutes": sum(
            w.duration for w in workouts
        )
    }


# 5. WORKOUT STREAK TRACKING
@router.get("/streak")
def get_workout_streak(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workout_dates = db.query(
        Workout.workout_date
    ).filter(
        Workout.user_id == current_user.id,
        Workout.workout_date <= date.today()
    ).distinct().order_by(
        Workout.workout_date.desc()
    ).all()

    dates = [row[0] for row in workout_dates]

    if not dates:
        return {
            "current_streak": 0,
            "longest_streak": 0,
            "total_active_days": 0
        }

    # Calculate longest streak
    longest_streak = 1
    streak = 1

    for i in range(1, len(dates)):
        if dates[i - 1] - dates[i] == timedelta(days=1):
            streak += 1
            longest_streak = max(longest_streak, streak)
        else:
            streak = 1

    # Calculate current streak
    today = date.today()
    current_streak = 0

    if dates[0] == today or dates[0] == today - timedelta(days=1):
        current_streak = 1

        for i in range(1, len(dates)):
            if dates[i - 1] - dates[i] == timedelta(days=1):
                current_streak += 1
            else:
                break

    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "total_active_days": len(dates)
    }


# 6. PERSONAL FITNESS DASHBOARD
@router.get("/dashboard")
def get_fitness_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workouts = db.query(Workout).filter(
        Workout.user_id == current_user.id
    )

    total_workouts = workouts.count()

    total_calories = workouts.with_entities(
        func.coalesce(
            func.sum(Workout.calories_burned), 0
        )
    ).scalar()

    total_duration = workouts.with_entities(
        func.coalesce(
            func.sum(Workout.duration), 0
        )
    ).scalar()

    latest_workout = workouts.order_by(
        Workout.workout_date.desc(),
        Workout.id.desc()
    ).first()

    return {
        "total_workouts": total_workouts,
        "total_calories": total_calories,
        "total_duration_minutes": total_duration,
        "latest_workout": (
            {
                "workout_name": latest_workout.workout_name,
                "category": latest_workout.category,
                "workout_date": latest_workout.workout_date
            }
            if latest_workout else None
        )
    }
