
from datetime import date

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import Workout, Progress, Streak


def sync_daily_progress(
    db: Session,
    user_id: int,
    workout_date: date
):
    db.flush()

    total_workouts = db.query(Workout).filter(
        Workout.user_id == user_id,
        Workout.workout_date == workout_date
    ).count()

    total_calories = db.query(
        func.coalesce(func.sum(Workout.calories_burned), 0)
    ).filter(
        Workout.user_id == user_id,
        Workout.workout_date == workout_date
    ).scalar() or 0

    progress = db.query(Progress).filter(
        Progress.user_id == user_id,
        Progress.date == workout_date
    ).first()

    if total_workouts == 0:
        if progress:
            db.delete(progress)

    elif progress:
        progress.total_workouts = total_workouts
        progress.total_calories = total_calories

    else:
        progress = Progress(
            user_id=user_id,
            total_workouts=total_workouts,
            total_calories=total_calories,
            date=workout_date
        )
        db.add(progress)


def sync_workout_streak(
    db: Session,
    user_id: int
):
    db.flush()

    today = date.today()

    dates = db.query(
        Workout.workout_date
    ).filter(
        Workout.user_id == user_id,
        Workout.workout_date <= today
    ).distinct().order_by(
        Workout.workout_date.asc()
    ).all()

    workout_dates = [row[0] for row in dates]

    # Calculate longest streak
    longest_streak = 0
    current_run = 0
    previous_date = None

    for workout_date in workout_dates:
        if (
            previous_date is not None
            and (workout_date - previous_date).days == 1
        ):
            current_run += 1
        else:
            current_run = 1

        longest_streak = max(longest_streak, current_run)
        previous_date = workout_date

    # Calculate current streak
    current_streak = 0

    if workout_dates:
        last_date = workout_dates[-1]

        if (today - last_date).days <= 1:
            current_streak = 1

            for i in range(len(workout_dates) - 1, 0, -1):
                if (
                    workout_dates[i] - workout_dates[i - 1]
                ).days == 1:
                    current_streak += 1
                else:
                    break

    # Find or create streak record
    streak = db.query(Streak).filter(
        Streak.user_id == user_id
    ).first()

    if streak is None:
        streak = Streak(user_id=user_id)
        db.add(streak)

    streak.current_streak = current_streak
    streak.longest_streak = longest_streak
    streak.last_workout_date = (
        workout_dates[-1] if workout_dates else None
    )
