
from datetime import date, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.database import get_db
from app.models import (
    Workout,
    User,
    Streak,
    Goal,
    WorkoutPlan,
    Badge
)
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/dashboard",
    tags=["Fitness Dashboard"]
)


# 1. DASHBOARD SUMMARY
@router.get("/summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total_workouts = db.query(
        func.count(Workout.id)
    ).filter(
        Workout.user_id == current_user.id
    ).scalar() or 0

    total_calories = db.query(
        func.coalesce(func.sum(Workout.calories_burned), 0)
    ).filter(
        Workout.user_id == current_user.id
    ).scalar() or 0

    total_duration = db.query(
        func.coalesce(func.sum(Workout.duration), 0)
    ).filter(
        Workout.user_id == current_user.id
    ).scalar() or 0

    return {
        "total_workouts": total_workouts,
        "total_calories": total_calories,
        "total_duration_minutes": total_duration
    }


# 2. WEEKLY ANALYTICS
@router.get("/weekly")
def weekly_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()
    start_date = today - timedelta(days=6)

    results = db.query(
        Workout.workout_date,
        func.count(Workout.id).label("total_workouts"),
        func.sum(Workout.calories_burned).label("total_calories"),
        func.sum(Workout.duration).label("total_duration")
    ).filter(
        Workout.user_id == current_user.id,
        Workout.workout_date >= start_date,
        Workout.workout_date <= today
    ).group_by(
        Workout.workout_date
    ).order_by(
        Workout.workout_date
    ).all()

    return [
        {
            "date": str(row.workout_date),
            "total_workouts": row.total_workouts,
            "total_calories": row.total_calories or 0,
            "total_duration": row.total_duration or 0
        }
        for row in results
    ]


# 3. CATEGORY ANALYTICS
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


# 4. MONTHLY ANALYTICS
@router.get("/monthly")
def monthly_analytics(
    year: int = Query(..., ge=2000, le=2100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = db.query(
        extract("month", Workout.workout_date).label("month"),
        func.count(Workout.id).label("total_workouts"),
        func.sum(Workout.calories_burned).label("total_calories"),
        func.sum(Workout.duration).label("total_duration")
    ).filter(
        Workout.user_id == current_user.id,
        extract("year", Workout.workout_date) == year
    ).group_by(
        extract("month", Workout.workout_date)
    ).order_by(
        extract("month", Workout.workout_date)
    ).all()

    return [
        {
            "month": int(row.month),
            "total_workouts": row.total_workouts,
            "total_calories": row.total_calories or 0,
            "total_duration": row.total_duration or 0
        }
        for row in results
    ]


# 5. WEEKLY PROGRESS COMPARISON
@router.get("/weekly-comparison")
def weekly_comparison(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()

    current_start = today - timedelta(days=6)
    previous_start = today - timedelta(days=13)
    previous_end = today - timedelta(days=7)

    def get_totals(start_date, end_date):
        result = db.query(
            func.count(Workout.id),
            func.coalesce(func.sum(Workout.calories_burned), 0),
            func.coalesce(func.sum(Workout.duration), 0)
        ).filter(
            Workout.user_id == current_user.id,
            Workout.workout_date >= start_date,
            Workout.workout_date <= end_date
        ).first()

        return {
            "total_workouts": result[0] or 0,
            "total_calories": result[1] or 0,
            "total_duration": result[2] or 0
        }

    current_week = get_totals(current_start, today)
    previous_week = get_totals(previous_start, previous_end)

    def calculate_change(current, previous):
        if previous == 0:
            return 100.0 if current > 0 else 0.0

        return round(
            ((current - previous) / previous) * 100,
            2
        )

    return {
        "current_week": current_week,
        "previous_week": previous_week,
        "improvement": {
            "workouts_percentage": calculate_change(
                current_week["total_workouts"],
                previous_week["total_workouts"]
            ),
            "calories_percentage": calculate_change(
                current_week["total_calories"],
                previous_week["total_calories"]
            ),
            "duration_percentage": calculate_change(
                current_week["total_duration"],
                previous_week["total_duration"]
            )
        }
    }


# 6. BASIC WORKOUT STREAK
@router.get("/streak")
def workout_streak(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dates = db.query(
        Workout.workout_date
    ).filter(
        Workout.user_id == current_user.id
    ).distinct().order_by(
        Workout.workout_date.desc()
    ).all()

    workout_dates = {row[0] for row in dates}

    streak = 0
    check_date = date.today()

    if check_date not in workout_dates:
        check_date -= timedelta(days=1)

    while check_date in workout_dates:
        streak += 1
        check_date -= timedelta(days=1)

    return {
        "current_streak": streak,
        "message": "Keep going! Stay consistent."
    }


# 7. DETAILED WORKOUT STREAK
@router.get("/streak-details")
def get_streak_details(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    streak = db.query(Streak).filter(
        Streak.user_id == current_user.id
    ).first()

    if streak is None:
        return {
            "current_streak": 0,
            "longest_streak": 0,
            "last_workout_date": None
        }

    return {
        "current_streak": streak.current_streak,
        "longest_streak": streak.longest_streak,
        "last_workout_date": streak.last_workout_date
    }


# 8. PERSONALIZED DASHBOARD OVERVIEW
@router.get("/overview")
def personalized_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()

    # Overall workout statistics
    total_workouts = db.query(
        func.count(Workout.id)
    ).filter(
        Workout.user_id == current_user.id
    ).scalar() or 0

    total_calories = db.query(
        func.coalesce(func.sum(Workout.calories_burned), 0)
    ).filter(
        Workout.user_id == current_user.id
    ).scalar() or 0

    total_duration = db.query(
        func.coalesce(func.sum(Workout.duration), 0)
    ).filter(
        Workout.user_id == current_user.id
    ).scalar() or 0

    # Streak information
    streak = db.query(Streak).filter(
        Streak.user_id == current_user.id
    ).first()

    streak_data = {
        "current_streak": streak.current_streak if streak else 0,
        "longest_streak": streak.longest_streak if streak else 0,
        "last_workout_date": (
            streak.last_workout_date if streak else None
        )
    }

    # Upcoming workout plans
    upcoming_plans = db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == current_user.id,
        WorkoutPlan.scheduled_date >= today
    ).order_by(
        WorkoutPlan.scheduled_date.asc()
    ).limit(5).all()

    plans_data = [
        {
            "id": plan.id,
            "title": plan.title,
            "description": plan.description,
            "scheduled_date": plan.scheduled_date
        }
        for plan in upcoming_plans
    ]

    # Goal progress
    goals = db.query(Goal).filter(
        Goal.user_id == current_user.id
    ).order_by(
        Goal.deadline.asc()
    ).all()

    goals_data = []

    for goal in goals:
        percentage = round(
            (goal.current_value / goal.target_value) * 100,
            2
        ) if goal.target_value > 0 else 0

        goals_data.append({
            "id": goal.id,
            "goal_type": goal.goal_type,
            "target_value": goal.target_value,
            "current_value": goal.current_value,
            "progress_percentage": percentage,
            "deadline": goal.deadline,
            "completed": goal.current_value >= goal.target_value
        })

    # Achievement badges
    badges = db.query(Badge).filter(
        Badge.user_id == current_user.id
    ).order_by(
        Badge.earned_at.desc()
    ).all()

    badges_data = [
        {
            "id": badge.id,
            "badge_name": badge.badge_name,
            "description": badge.description,
            "earned_at": badge.earned_at
        }
        for badge in badges
    ]

    return {
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email
        },
        "workout_summary": {
            "total_workouts": total_workouts,
            "total_calories": total_calories,
            "total_duration_minutes": total_duration
        },
        "streak": streak_data,
        "upcoming_workout_plans": plans_data,
        "goals": goals_data,
        "achievement_badges": badges_data
    }
